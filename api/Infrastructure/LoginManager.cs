using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Localization;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace Carnavacs.Api.Infrastructure
{
    public class LoginManager
    {
        private readonly IConfiguration _config;
        private readonly IUnitOfWork _unitOfWork;
        private readonly TokenHandler _tokenHandler;


        public LoginManager(IConfiguration config, IUnitOfWork unitOfWork, TokenHandler tokenHandler)
        {
            _config = config;
            _unitOfWork = unitOfWork;
            _tokenHandler = tokenHandler;
        }

        public  User Login(LoginModel login)
        {
            return new User { Email = "test@test.com", Name = "Test User" };
        }

        //public async Task<(LoginResponse? response, string message)> Login(LoginModel login)
        //{
        //    try
        //    {
        //        var userWithProfile = await _unitOfWork.Users.GetUserByUserAndPassword(login.Username, login.Password);
        //        if (userWithProfile != null)
        //        {
        //            var userModel = new UserModel(userWithProfile);

        //            List<TwoFactorType> availableMethods = userWithProfile.Organization.GetMFaMethods();

        //            TwoFactor mfaSettings = new TwoFactor
        //            {
        //                AvailableMethods = availableMethods,
        //                DefaultMethod = TwoFactorType.FromValue(userWithProfile.Organization.Default2Fa),
        //                Method = userModel.TwoFactorMethod,
        //                CodeRequired = userModel.TwoFactorMethod != TwoFactorType.None && !availableMethods.Exists(x => x.Id == TwoFactorType.None.Id),
        //                Ingore2fa = login.Ingore2fa,
        //                hasApp = !string.IsNullOrEmpty(userWithProfile.Mfasecret),
        //                OrganizationLoginMessage = userWithProfile.Organization.TwoFAContactEn
        //            };

        //            if (mfaSettings.DefaultMethod == TwoFactorType.App)
        //                mfaSettings.ActivationDate = userWithProfile.Organization.TwoFaappActivationDate;
        //            else if (mfaSettings.DefaultMethod == TwoFactorType.Email)
        //            {
        //                mfaSettings.ActivationDate = userWithProfile.Organization.TwoFaemailActivationDate;
        //            }

        //            if (!string.IsNullOrEmpty(login.Force2FaMethod))
        //            {
        //                if (!availableMethods.Exists(x => x.Id == login.Force2FaMethod))
        //                    return (null, "Invalid 2Fa Method");

        //                if (login.Force2FaMethod == TwoFactorType.Email.Id)
        //                {
        //                    mfaSettings.Method = TwoFactorType.Email;
        //                    userModel.TwoFactorMethod = TwoFactorType.Email;
        //                }
        //            }

        //            bool isEmail2FaRequired = !login.Ingore2fa && !userModel.FirstLogin
        //                    && ((userWithProfile.Mfatype == TwoFactorType.Email.Id || login.Force2FaMethod == TwoFactorType.Email.Id) && availableMethods.Exists(x => x.Id == TwoFactorType.Email.Id));
        //            if (isEmail2FaRequired)
        //            {
        //                if (string.IsNullOrEmpty(login.VerificationCode))
        //                {
        //                    userModel.Secret = await _securityManager.Send2FaByEmail(userWithProfile);
        //                }
        //                else
        //                {
        //                    var generatedCode = contextAccessor.HttpContext.User.FindFirst("Secret").Value;
        //                    userModel.Secret = generatedCode;
        //                }
        //            }

        //            var token = string.Empty;
        //            var refreshToken = string.Empty;
        //            int duration = mfaSettings.Validate2fa(userModel, login.VerificationCode);
        //            token = tokenManager.BuildToken(userModel, login.Password, duration);
        //            refreshToken = BuildRefreshToken(userModel);
        //            var setting = _centralManager.Usersetting(1, userModel);
        //            var appMenus = _centralManager.GetMenusForProfile(userWithProfile);
        //            var nav = new List<NavigationViewModel>();
        //            var menu = _mapper.Map(appMenus, nav);
        //            var tree = _centralManager.RawCollectionToTree(menu).ToList();

        //            _securityManager.Audit(AuditActionsEnum.Login, userWithProfile.Id);
        //            await _iTSCentralContext.SaveChangesAsync();
        //            return (new ResponseLogin
        //            {
        //                access_token = token,
        //                user = setting,
        //                navigation = tree,
        //                refresh_token = refreshToken,
        //                TwoFactor = mfaSettings
        //            }, string.Empty); ;
        //        }
        //        else
        //        {
        //            throw new Exception(Resource.InvalidUser);
        //        }
        //    }
        //    catch (System.Exception ex)
        //    {
        //        throw new Exception(Resource.ErrorGettingUser);
        //    }
        //}

        //public String GetClaimValue(String t, String ClaimType)
        //{
        //    t = t.Replace("Bearer ", "");
        //    var mySecret = _config["Jwt:Key"];
        //    var mySecurityKey = new SymmetricSecurityKey(Encoding.ASCII.GetBytes(mySecret));

        //    var myIssuer = _config["Jwt:Issuer"];
        //    var myAudience = _config["Jwt:Issuer"];

        //    var tokenHandler = new JwtSecurityTokenHandler();

        //    var x = tokenHandler.ValidateToken(t, new TokenValidationParameters
        //    {
        //        ValidateIssuerSigningKey = true,
        //        ValidateIssuer = true,
        //        ValidateAudience = true,
        //        ValidIssuer = myIssuer,
        //        ValidAudience = myAudience,
        //        IssuerSigningKey = mySecurityKey
        //    }, out SecurityToken validatedToken);
        //    return x.Claims.Where(x => x.Type == ClaimType).First().Value;
        //}

        //private string BuildRefreshToken(UserModel user)
        //{
        //    var refreshTokenClaims = new List<Claim>
        //    {
        //        new Claim(JwtRegisteredClaimNames.Sub, user.id.ToString()),
        //        new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        //    };

        //    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]));
        //    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        //    var refreshToken = new JwtSecurityToken(
        //        _config["Jwt:Issuer"],
        //        _config["Jwt:Issuer"],
        //        refreshTokenClaims,
        //        expires: DateTime.Now.AddDays(30),
        //        signingCredentials: creds);

        //    return new JwtSecurityTokenHandler().WriteToken(refreshToken);
        //}

        //public async Task<(string access_token, string refresh_token)> RenewToken([FromBody] RefreshTokenRequest tokenRequest)
        //{
        //    var tokenHandler = new Intechsol.Elysium.Common.TokenHandler();
        //    try
        //    {
        //        var validatedToken = ValidateRefreshToken(tokenRequest.RefreshToken);
        //        if (validatedToken == null)
        //            return (null, null);

        //        var userName = validatedToken.Claims.Where(x => x.Type == "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name").FirstOrDefault().Value;

        //        var user = _securityManager.GetUserByUsername(userName);
        //        var userModel = new UserModel(user);

        //        if (user != null)
        //        {
        //            var newAccessToken = tokenHandler.BuildToken(userModel);
        //            var newRefreshToken = BuildRefreshToken(userModel);

        //            return (newAccessToken, newRefreshToken);
        //        }

        //        return (null, null);
        //    }
        //    catch (Exception ex)
        //    {
        //        return (null, null);
        //    }
        //}

        //private ClaimsPrincipal ValidateRefreshToken(string refreshToken)
        //{
        //    var tokenHandler = new JwtSecurityTokenHandler();
        //    var key = Encoding.ASCII.GetBytes(_config["Jwt:Key"]);

        //    try
        //    {
        //        var principal = tokenHandler.ValidateToken(refreshToken, new TokenValidationParameters
        //        {
        //            ValidateIssuerSigningKey = true,
        //            IssuerSigningKey = new SymmetricSecurityKey(key),
        //            ValidateIssuer = true,
        //            ValidateAudience = true,
        //        }, out SecurityToken validatedToken);

        //        return principal;
        //    }
        //    catch
        //    {
        //        return null;
        //    }
        //}


    }

}
