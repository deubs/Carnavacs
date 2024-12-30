using Carnavacs.Api.Domain.Entities;
using Microsoft.IdentityModel.Tokens;
using System.Collections.Specialized;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace Carnavacs.Api.Infrastructure
{
    public class TokenHandler
    {
        private IConfiguration _config;

        public TokenHandler(IConfiguration config) {
            _config = config;
        }

        public string BuildToken(User user, int validMinutes = 60 * 24 * 7)
        {
            var secretKey = _config["Jwt:Key"];
            var issuer = _config["Jwt:Issuer"];
            List<Claim> claims = new List<Claim>();
            claims.Add(new Claim(JwtRegisteredClaimNames.NameId, user.Id.ToString()));
            claims.Add(new Claim(JwtRegisteredClaimNames.UniqueName, user.UserName));
            claims.Add(new Claim(JwtRegisteredClaimNames.Sub, user.Name));
            claims.Add(new Claim(JwtRegisteredClaimNames.Email, user.Email));
            claims.Add(new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()));



            if (user.Roles != null)
                foreach (string role in user.Roles)
                {
                    claims.Add(new Claim(ClaimTypes.Role, role));
                }

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer,
                issuer,
                claims,
               expires: DateTime.Now.AddMinutes(validMinutes),
               signingCredentials: creds);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }


        public String GetClaimValue(String t, String ClaimType)
        {
            return Decode(t).Claims.Where(x => x.Type == ClaimType).First().Value;
        }

        public ClaimsPrincipal Decode(string token)
        {
            SecurityToken validatedToken = null;
            token = token.Replace("Bearer ", "");
            var secretKey = _config["Jwt:Key"];
            var issuer = _config["Jwt:Issuer"];
            var mySecurityKey = new SymmetricSecurityKey(Encoding.ASCII.GetBytes(secretKey));

            var myIssuer = issuer;
            var myAudience = issuer;

            var tokenHandler = new JwtSecurityTokenHandler();

            try
            {
                var x = tokenHandler.ValidateToken(token, new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidIssuer = myIssuer,
                    ValidAudience = myAudience,
                    IssuerSigningKey = mySecurityKey
                }, out validatedToken);
                return x;
            }
            catch
            {

            }
            return null;
        }
    }
}
